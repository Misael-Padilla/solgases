from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from apps.insumos.models import Insumo
from apps.productos.models import Producto
from apps.usuarios.models import Cliente, Proveedor, Usuario

from .models import DetalleVenta, FacturaVenta


# ─── Factories ────────────────────────────────────────────────────────────────
# Funciones que construyen instancias válidas mínimas de cada modelo.
# Usar funciones (no fixtures globales) evita estado oculto entre tests.

def make_usuario(correo='vendedor@solgases.com', identificacion='11111111'):
    return Usuario.objects.create_user(
        correo_electronico=correo,
        password='testpass123',
        tipo_identificacion='CC',
        identificacion=identificacion,
        nombres='Vendedor',
        apellidos='Prueba',
        telefono='3000000000',
        direccion='Calle 1 # 1-1',
        ciudad='Bogotá',
        departamento='Cundinamarca',
        rol='EMP',
    )


def make_cliente(identificacion='22222222'):
    return Cliente.objects.create(
        tipo_identificacion='CC',
        identificacion=identificacion,
        nombres='Juan',
        apellidos='Pérez',
        telefono='3001111111',
        direccion='Carrera 5 # 10-20',
        ciudad='Bogotá',
        departamento='Cundinamarca',
    )


def make_proveedor(identificacion='900100200'):
    return Proveedor.objects.create(
        tipo_identificacion='NIT',
        identificacion=identificacion,
        razon_social='Gases Industriales S.A.S.',
        telefono='3002222222',
        direccion='Zona Industrial',
        ciudad='Medellín',
        departamento='Antioquia',
    )


def make_factura_venta(usuario, cliente, numero='FV-0001'):
    return FacturaVenta.objects.create(
        numero_factura=numero,
        cliente=cliente,
        registrado_por=usuario,
        fecha_factura=timezone.now(),
        metodo_pago='EFECTIVO',
        subtotal=Decimal('10000.00'),
        iva_porcentaje=Decimal('19.00'),
        iva=Decimal('1900.00'),
        total=Decimal('11900.00'),
    )


def make_detalle(factura, tipo, codigo, descripcion, cantidad, precio_unitario):
    """Crea DetalleVenta y activa la lógica de descuento de stock en save()."""
    return DetalleVenta.objects.create(
        factura_venta=factura,
        tipo_item=tipo,
        codigo_item=codigo,
        descripcion=descripcion,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        subtotal=precio_unitario * cantidad,
    )


# ─── Tests: DetalleVenta con PRODUCTO ────────────────────────────────────────

class DetalleVentaProductoTest(TestCase):
    """
    Cubre la lógica de DetalleVenta.save() para ítems de tipo PRODUCTO:
    descuento de stock, validación de disponibilidad y rollback atómico.
    """

    @classmethod
    def setUpTestData(cls):
        # Datos de apoyo que no cambian — se crean una sola vez para toda la clase
        cls.usuario = make_usuario()
        cls.cliente = make_cliente()

    def setUp(self):
        # Producto se crea en cada test porque el stock se modifica
        self.producto = Producto.objects.create(
            codigo='PROD-001',
            nombre='Casco de Seguridad',
            categoria='EPP',
            genero='Unisex',
            precio_compra=Decimal('10000.00'),
            precio_venta=Decimal('15000.00'),
            stock=10,
            stock_minimo=3,
            stock_maximo=20,
        )
        self.factura = make_factura_venta(self.usuario, self.cliente)

    # ── Happy path ────────────────────────────────────────────────────────────

    def test_stock_disminuye_en_cantidad_vendida(self):
        """El stock del producto debe reducirse exactamente en la cantidad del detalle."""
        make_detalle(self.factura, 'PRODUCTO', 'PROD-001', 'Casco', 3, Decimal('15000.00'))
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 7)

    def test_vender_todo_el_stock_disponible_lleva_a_cero(self):
        """Vender exactamente el stock disponible debe dejarlo en 0 sin lanzar error."""
        make_detalle(self.factura, 'PRODUCTO', 'PROD-001', 'Casco', 10, Decimal('15000.00'))
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 0)

    def test_detalle_se_persiste_en_base_de_datos(self):
        """El DetalleVenta debe quedar guardado cuando la venta es válida."""
        make_detalle(self.factura, 'PRODUCTO', 'PROD-001', 'Casco', 2, Decimal('15000.00'))
        self.assertEqual(DetalleVenta.objects.count(), 1)

    # ── Error cases ───────────────────────────────────────────────────────────

    def test_lanza_error_si_cantidad_supera_stock_disponible(self):
        """Intentar vender más unidades de las disponibles debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            make_detalle(self.factura, 'PRODUCTO', 'PROD-001', 'Casco', 15, Decimal('15000.00'))

    def test_mensaje_error_contiene_nombre_del_producto(self):
        """El ValueError debe identificar el producto afectado para facilitar diagnóstico."""
        with self.assertRaises(ValueError) as ctx:
            make_detalle(self.factura, 'PRODUCTO', 'PROD-001', 'Casco', 15, Decimal('15000.00'))
        self.assertIn('Casco de Seguridad', str(ctx.exception))

    def test_lanza_error_si_codigo_producto_no_existe(self):
        """Un código de producto inexistente debe lanzar ValueError, no DoesNotExist."""
        with self.assertRaises(ValueError):
            make_detalle(self.factura, 'PRODUCTO', 'XXXX-999', 'Fantasma', 1, Decimal('10000.00'))

    # ── Rollback atómico ──────────────────────────────────────────────────────

    def test_stock_no_cambia_si_la_venta_falla(self):
        """
        Si la venta falla por stock insuficiente, transaction.atomic() revierte
        el cambio — el stock debe quedar idéntico al estado inicial.
        """
        stock_antes = self.producto.stock
        try:
            make_detalle(self.factura, 'PRODUCTO', 'PROD-001', 'Casco', 50, Decimal('15000.00'))
        except ValueError:
            pass
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, stock_antes)

    def test_detalle_no_se_persiste_si_stock_insuficiente(self):
        """Si el stock falla, el DetalleVenta tampoco debe guardarse en base de datos."""
        try:
            make_detalle(self.factura, 'PRODUCTO', 'PROD-001', 'Casco', 50, Decimal('15000.00'))
        except ValueError:
            pass
        self.assertEqual(DetalleVenta.objects.count(), 0)


# ─── Tests: DetalleVenta con INSUMO ──────────────────────────────────────────

class DetalleVentaInsumoTest(TestCase):
    """
    Cubre la lógica de DetalleVenta.save() para ítems de tipo INSUMO:
    descuento de stock, validación de disponibilidad y rollback atómico.
    """

    @classmethod
    def setUpTestData(cls):
        cls.usuario = make_usuario()
        cls.cliente = make_cliente()
        cls.proveedor = make_proveedor()

    def setUp(self):
        self.insumo = Insumo.objects.create(
            codigo='INS-001',
            nombre='Oxígeno Industrial',
            subcategoria='GAS',
            unidad_medida='Litros',
            precio_compra=Decimal('5000.00'),
            stock=8,
            stock_minimo=2,
            stock_maximo=15,
            proveedor=self.proveedor,
        )
        self.factura = make_factura_venta(self.usuario, self.cliente)

    # ── Happy path ────────────────────────────────────────────────────────────

    def test_stock_insumo_disminuye_en_cantidad_vendida(self):
        """El stock del insumo debe reducirse exactamente en la cantidad del detalle."""
        make_detalle(self.factura, 'INSUMO', 'INS-001', 'Oxígeno', 3, Decimal('5000.00'))
        self.insumo.refresh_from_db()
        self.assertEqual(self.insumo.stock, 5)

    def test_vender_todo_el_stock_insumo_lleva_a_cero(self):
        """Vender exactamente el stock disponible de insumo debe dejarlo en 0."""
        make_detalle(self.factura, 'INSUMO', 'INS-001', 'Oxígeno', 8, Decimal('5000.00'))
        self.insumo.refresh_from_db()
        self.assertEqual(self.insumo.stock, 0)

    # ── Error cases ───────────────────────────────────────────────────────────

    def test_lanza_error_si_stock_insumo_insuficiente(self):
        """Vender más insumo del disponible debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            make_detalle(self.factura, 'INSUMO', 'INS-001', 'Oxígeno', 20, Decimal('5000.00'))

    def test_lanza_error_si_codigo_insumo_no_existe(self):
        """Un código de insumo inexistente debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            make_detalle(self.factura, 'INSUMO', 'XXXX-000', 'Fantasma', 1, Decimal('1000.00'))

    # ── Rollback atómico ──────────────────────────────────────────────────────

    def test_stock_insumo_no_cambia_si_la_venta_falla(self):
        """La transacción atómica debe revertir el stock si la venta de insumo falla."""
        stock_antes = self.insumo.stock
        try:
            make_detalle(self.factura, 'INSUMO', 'INS-001', 'Oxígeno', 100, Decimal('5000.00'))
        except ValueError:
            pass
        self.insumo.refresh_from_db()
        self.assertEqual(self.insumo.stock, stock_antes)

    def test_detalle_insumo_no_se_persiste_si_stock_insuficiente(self):
        """Si el stock de insumo falla, el DetalleVenta no debe guardarse."""
        try:
            make_detalle(self.factura, 'INSUMO', 'INS-001', 'Oxígeno', 100, Decimal('5000.00'))
        except ValueError:
            pass
        self.assertEqual(DetalleVenta.objects.count(), 0)

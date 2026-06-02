from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from apps.insumos.models import Insumo
from apps.productos.models import Producto
from apps.usuarios.models import Proveedor, Usuario

from .models import DetalleCompra, FacturaCompra


# ─── Factories ────────────────────────────────────────────────────────────────

def make_usuario(correo='compras@solgases.com', identificacion='33333333'):
    return Usuario.objects.create_user(
        correo_electronico=correo,
        password='testpass123',
        tipo_identificacion='CC',
        identificacion=identificacion,
        nombres='Comprador',
        apellidos='Prueba',
        telefono='3003333333',
        direccion='Calle 3 # 3-3',
        ciudad='Bogotá',
        departamento='Cundinamarca',
        rol='EMP',
    )


def make_proveedor(identificacion='900300400'):
    return Proveedor.objects.create(
        tipo_identificacion='NIT',
        identificacion=identificacion,
        razon_social='Distribuidora Industrial S.A.S.',
        telefono='3004444444',
        direccion='Zona Industrial Km 2',
        ciudad='Cali',
        departamento='Valle del Cauca',
    )


def make_factura_compra(usuario, proveedor, numero='FC-0001'):
    return FacturaCompra.objects.create(
        numero_factura=numero,
        proveedor=proveedor,
        registrado_por=usuario,
        fecha_factura=timezone.now(),
        subtotal=Decimal('50000.00'),
        iva_porcentaje=Decimal('19.00'),
        iva=Decimal('9500.00'),
        total=Decimal('59500.00'),
    )


def make_detalle(factura, tipo, codigo, descripcion, cantidad, precio_unitario):
    """Crea DetalleCompra y activa la lógica de actualización de stock en save()."""
    return DetalleCompra.objects.create(
        factura_compra=factura,
        tipo_item=tipo,
        codigo_item=codigo,
        descripcion=descripcion,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        subtotal=precio_unitario * cantidad,
    )


# ─── Tests: DetalleCompra con PRODUCTO ───────────────────────────────────────

class DetalleCompraProductoTest(TestCase):
    """
    Cubre la lógica de DetalleCompra.save() para ítems de tipo PRODUCTO:
    aumento de stock, actualización de precio y creación automática del producto.
    """

    @classmethod
    def setUpTestData(cls):
        cls.usuario = make_usuario()
        cls.proveedor = make_proveedor()

    def setUp(self):
        self.producto = Producto.objects.create(
            codigo='PROD-001',
            nombre='Guantes de Cuero',
            categoria='EPP',
            genero='Unisex',
            precio_compra=Decimal('8000.00'),
            precio_venta=Decimal('12000.00'),
            stock=5,
            stock_minimo=2,
            stock_maximo=30,
        )
        self.factura = make_factura_compra(self.usuario, self.proveedor)

    # ── Happy path ────────────────────────────────────────────────────────────

    def test_stock_aumenta_en_cantidad_comprada(self):
        """El stock del producto debe incrementarse exactamente en la cantidad del detalle."""
        make_detalle(self.factura, 'PRODUCTO', 'PROD-001', 'Guantes', 10, Decimal('7500.00'))
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 15)

    def test_precio_compra_se_actualiza_con_nuevo_valor(self):
        """El precio de compra del producto debe actualizarse al valor de la factura."""
        nuevo_precio = Decimal('7500.00')
        make_detalle(self.factura, 'PRODUCTO', 'PROD-001', 'Guantes', 5, nuevo_precio)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.precio_compra, nuevo_precio)

    def test_detalle_se_persiste_en_base_de_datos(self):
        """El DetalleCompra debe quedar guardado en base de datos."""
        make_detalle(self.factura, 'PRODUCTO', 'PROD-001', 'Guantes', 5, Decimal('7500.00'))
        self.assertEqual(DetalleCompra.objects.count(), 1)

    # ── Auto-creación ─────────────────────────────────────────────────────────

    def test_producto_inexistente_se_crea_automaticamente(self):
        """Si el código no existe, DetalleCompra debe crear el Producto automáticamente."""
        make_detalle(self.factura, 'PRODUCTO', 'PROD-NUEVO', 'Bota Industrial', 20, Decimal('25000.00'))
        self.assertTrue(Producto.objects.filter(codigo='PROD-NUEVO').exists())

    def test_producto_creado_tiene_stock_de_la_compra(self):
        """El producto creado automáticamente debe tener como stock la cantidad comprada."""
        make_detalle(self.factura, 'PRODUCTO', 'PROD-NUEVO', 'Bota Industrial', 20, Decimal('25000.00'))
        producto = Producto.objects.get(codigo='PROD-NUEVO')
        self.assertEqual(producto.stock, 20)

    def test_producto_creado_tiene_nombre_de_la_descripcion(self):
        """El nombre del producto creado automáticamente debe venir de la descripción del detalle."""
        make_detalle(self.factura, 'PRODUCTO', 'PROD-NUEVO', 'Bota Industrial', 5, Decimal('25000.00'))
        producto = Producto.objects.get(codigo='PROD-NUEVO')
        self.assertEqual(producto.nombre, 'Bota Industrial')

    def test_producto_creado_tiene_precio_compra_correcto(self):
        """El precio de compra del producto creado debe ser el precio unitario del detalle."""
        precio = Decimal('25000.00')
        make_detalle(self.factura, 'PRODUCTO', 'PROD-NUEVO', 'Bota Industrial', 5, precio)
        producto = Producto.objects.get(codigo='PROD-NUEVO')
        self.assertEqual(producto.precio_compra, precio)


# ─── Tests: DetalleCompra con INSUMO ─────────────────────────────────────────

class DetalleCompraInsumoTest(TestCase):
    """
    Cubre la lógica de DetalleCompra.save() para ítems de tipo INSUMO:
    aumento de stock, actualización de precio y creación automática del insumo.
    """

    @classmethod
    def setUpTestData(cls):
        cls.usuario = make_usuario()
        cls.proveedor = make_proveedor()

    def setUp(self):
        self.insumo = Insumo.objects.create(
            codigo='INS-001',
            nombre='Nitrógeno Industrial',
            subcategoria='GAS',
            unidad_medida='Kilos',
            precio_compra=Decimal('12000.00'),
            stock=10,
            stock_minimo=3,
            stock_maximo=50,
            proveedor=self.proveedor,
        )
        self.factura = make_factura_compra(self.usuario, self.proveedor)

    # ── Happy path ────────────────────────────────────────────────────────────

    def test_stock_insumo_aumenta_en_cantidad_comprada(self):
        """El stock del insumo debe incrementarse exactamente en la cantidad del detalle."""
        make_detalle(self.factura, 'INSUMO', 'INS-001', 'Nitrógeno', 15, Decimal('11500.00'))
        self.insumo.refresh_from_db()
        self.assertEqual(self.insumo.stock, 25)

    def test_precio_compra_insumo_se_actualiza(self):
        """El precio de compra del insumo debe actualizarse al valor de la factura."""
        nuevo_precio = Decimal('11500.00')
        make_detalle(self.factura, 'INSUMO', 'INS-001', 'Nitrógeno', 10, nuevo_precio)
        self.insumo.refresh_from_db()
        self.assertEqual(self.insumo.precio_compra, nuevo_precio)

    # ── Auto-creación ─────────────────────────────────────────────────────────

    def test_insumo_inexistente_se_crea_automaticamente(self):
        """Si el código no existe, DetalleCompra debe crear el Insumo automáticamente."""
        make_detalle(self.factura, 'INSUMO', 'INS-NUEVO', 'Argón Puro', 30, Decimal('9000.00'))
        self.assertTrue(Insumo.objects.filter(codigo='INS-NUEVO').exists())

    def test_insumo_creado_tiene_stock_de_la_compra(self):
        """El insumo creado automáticamente debe tener como stock la cantidad comprada."""
        make_detalle(self.factura, 'INSUMO', 'INS-NUEVO', 'Argón Puro', 30, Decimal('9000.00'))
        insumo = Insumo.objects.get(codigo='INS-NUEVO')
        self.assertEqual(insumo.stock, 30)

    def test_insumo_creado_tiene_proveedor_de_la_factura(self):
        """El insumo creado automáticamente debe quedar asociado al proveedor de la factura."""
        make_detalle(self.factura, 'INSUMO', 'INS-NUEVO', 'Argón Puro', 30, Decimal('9000.00'))
        insumo = Insumo.objects.get(codigo='INS-NUEVO')
        self.assertEqual(insumo.proveedor, self.proveedor)

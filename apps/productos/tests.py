from django.test import SimpleTestCase

from .models import Producto


def make_producto(stock, stock_minimo, stock_maximo):
    """Instancia Producto en memoria — nivel_stock no requiere persistencia en BD."""
    return Producto(
        codigo='TEST-001',
        nombre='Producto de Prueba',
        categoria='EPP',
        genero='Unisex',
        precio_compra='10000.00',
        precio_venta='15000.00',
        stock=stock,
        stock_minimo=stock_minimo,
        stock_maximo=stock_maximo,
    )


class ProductoNivelStockTest(SimpleTestCase):
    """
    Verifica la propiedad calculada nivel_stock del modelo Producto.
    Usa SimpleTestCase porque nivel_stock es lógica pura — no accede a la BD.
    Cubre los tres estados posibles y los cuatro valores de frontera.
    """

    # ── Estado BAJO ───────────────────────────────────────────────────────────

    def test_nivel_bajo_cuando_stock_igual_al_minimo(self):
        """Stock exactamente igual al mínimo debe retornar BAJO (frontera inferior)."""
        p = make_producto(stock=5, stock_minimo=5, stock_maximo=20)
        self.assertEqual(p.nivel_stock, 'BAJO')

    def test_nivel_bajo_cuando_stock_menor_al_minimo(self):
        """Stock por debajo del mínimo debe retornar BAJO."""
        p = make_producto(stock=2, stock_minimo=5, stock_maximo=20)
        self.assertEqual(p.nivel_stock, 'BAJO')

    def test_nivel_bajo_cuando_stock_es_cero(self):
        """Stock en cero siempre debe retornar BAJO independientemente del mínimo."""
        p = make_producto(stock=0, stock_minimo=5, stock_maximo=20)
        self.assertEqual(p.nivel_stock, 'BAJO')

    # ── Estado ALTO ───────────────────────────────────────────────────────────

    def test_nivel_alto_cuando_stock_igual_al_maximo(self):
        """Stock exactamente igual al máximo debe retornar ALTO (frontera superior)."""
        p = make_producto(stock=20, stock_minimo=5, stock_maximo=20)
        self.assertEqual(p.nivel_stock, 'ALTO')

    def test_nivel_alto_cuando_stock_supera_el_maximo(self):
        """Stock por encima del máximo debe retornar ALTO."""
        p = make_producto(stock=25, stock_minimo=5, stock_maximo=20)
        self.assertEqual(p.nivel_stock, 'ALTO')

    # ── Estado NORMAL ─────────────────────────────────────────────────────────

    def test_nivel_normal_entre_umbrales(self):
        """Stock entre mínimo y máximo (sin tocarlos) debe retornar NORMAL."""
        p = make_producto(stock=12, stock_minimo=5, stock_maximo=20)
        self.assertEqual(p.nivel_stock, 'NORMAL')

    def test_nivel_normal_justo_por_encima_del_minimo(self):
        """Stock en mínimo+1 debe retornar NORMAL, no BAJO (frontera inferior)."""
        p = make_producto(stock=6, stock_minimo=5, stock_maximo=20)
        self.assertEqual(p.nivel_stock, 'NORMAL')

    def test_nivel_normal_justo_por_debajo_del_maximo(self):
        """Stock en máximo-1 debe retornar NORMAL, no ALTO (frontera superior)."""
        p = make_producto(stock=19, stock_minimo=5, stock_maximo=20)
        self.assertEqual(p.nivel_stock, 'NORMAL')

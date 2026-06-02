from django.test import SimpleTestCase

from .models import Insumo


def make_insumo(stock, stock_minimo, stock_maximo):
    """Instancia Insumo en memoria — nivel_stock no requiere persistencia en BD."""
    return Insumo(
        codigo='INS-TEST',
        nombre='Insumo de Prueba',
        subcategoria='GAS',
        unidad_medida='Litros',
        precio_compra='5000.00',
        stock=stock,
        stock_minimo=stock_minimo,
        stock_maximo=stock_maximo,
    )


class InsumoNivelStockTest(SimpleTestCase):
    """
    Verifica la propiedad calculada nivel_stock del modelo Insumo.
    Usa SimpleTestCase porque nivel_stock es lógica pura — no accede a la BD.
    Cubre los tres estados posibles y los valores de frontera críticos.
    """

    # ── Estado BAJO ───────────────────────────────────────────────────────────

    def test_nivel_bajo_cuando_stock_igual_al_minimo(self):
        """Stock exactamente igual al mínimo debe retornar BAJO (frontera inferior)."""
        ins = make_insumo(stock=3, stock_minimo=3, stock_maximo=15)
        self.assertEqual(ins.nivel_stock, 'BAJO')

    def test_nivel_bajo_cuando_stock_menor_al_minimo(self):
        """Stock por debajo del mínimo debe retornar BAJO."""
        ins = make_insumo(stock=1, stock_minimo=3, stock_maximo=15)
        self.assertEqual(ins.nivel_stock, 'BAJO')

    # ── Estado ALTO ───────────────────────────────────────────────────────────

    def test_nivel_alto_cuando_stock_igual_al_maximo(self):
        """Stock exactamente igual al máximo debe retornar ALTO (frontera superior)."""
        ins = make_insumo(stock=15, stock_minimo=3, stock_maximo=15)
        self.assertEqual(ins.nivel_stock, 'ALTO')

    def test_nivel_alto_cuando_stock_supera_el_maximo(self):
        """Stock por encima del máximo debe retornar ALTO."""
        ins = make_insumo(stock=20, stock_minimo=3, stock_maximo=15)
        self.assertEqual(ins.nivel_stock, 'ALTO')

    # ── Estado NORMAL ─────────────────────────────────────────────────────────

    def test_nivel_normal_entre_umbrales(self):
        """Stock entre mínimo y máximo (sin tocarlos) debe retornar NORMAL."""
        ins = make_insumo(stock=8, stock_minimo=3, stock_maximo=15)
        self.assertEqual(ins.nivel_stock, 'NORMAL')

    def test_nivel_normal_justo_por_encima_del_minimo(self):
        """Stock en mínimo+1 debe retornar NORMAL, no BAJO."""
        ins = make_insumo(stock=4, stock_minimo=3, stock_maximo=15)
        self.assertEqual(ins.nivel_stock, 'NORMAL')

    def test_nivel_normal_justo_por_debajo_del_maximo(self):
        """Stock en máximo-1 debe retornar NORMAL, no ALTO."""
        ins = make_insumo(stock=14, stock_minimo=3, stock_maximo=15)
        self.assertEqual(ins.nivel_stock, 'NORMAL')

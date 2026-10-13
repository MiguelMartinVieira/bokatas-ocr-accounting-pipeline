"""
Standalone Demo & Test for Bokatas Ingestion Pipeline.
Simulates multimodal structured extraction and Pydantic validation.
"""

import json
from schema import DatosFacturaBokatas, LineaGastoCategoria, CategoriaBokatas

MOCK_EXTRACTED_PAYLOAD = {
    "fecha_factura": "2026-03-12",
    "sede": "Madrid-Centro",
    "proveedor": "Mercadona",
    "cif_nif_proveedor": "A-46103834",
    "numero_factura": "T-049821",
    "importe_total": 48.75,
    "metodo_pago": "Tarjeta",
    "desglose_categorias": [
        {
            "categoria": "Panadería",
            "concepto": "Barra de pan rústica 250g (Pack 5)",
            "cantidad": 4.0,
            "precio_unitario": 1.25,
            "importe_linea": 5.00
        },
        {
            "categoria": "Embutidos",
            "concepto": "Jamón cocido extra lonchas 400g",
            "cantidad": 6.0,
            "precio_unitario": 2.80,
            "importe_linea": 16.80
        },
        {
            "categoria": "Quesos",
            "concepto": "Queso gouda semicurado lonchas 300g",
            "cantidad": 5.0,
            "precio_unitario": 2.50,
            "importe_linea": 12.50
        },
        {
            "categoria": "Bebidas",
            "concepto": "Caldo de pollo brick 1L",
            "cantidad": 6.0,
            "precio_unitario": 1.15,
            "importe_linea": 6.90
        },
        {
            "categoria": "Desechables y Enseres",
            "concepto": "Servilletas papel celulosa 100u",
            "cantidad": 3.0,
            "precio_unitario": 1.20,
            "importe_linea": 3.60
        },
        {
            "categoria": "Desechables y Enseres",
            "concepto": "Bolsas isotérmicas reutilizables",
            "cantidad": 2.0,
            "precio_unitario": 1.975,
            "importe_linea": 3.95
        }
    ],
    "observaciones": "Thermal ticket slightly degraded at bottom margin. Arithmetic verified."
}

def test_pipeline_validation():
    # 1. Parse into strict Pydantic model
    factura = DatosFacturaBokatas.model_validate(MOCK_EXTRACTED_PAYLOAD)
    
    # 2. Arithmetic invariant verification
    total_lineas = sum(item.importe_linea for item in factura.desglose_categorias)
    assert round(total_lineas, 2) == round(factura.importe_total, 2), "Invoice totals do not balance!"
    
    # 3. Assert all categories are strictly within official 9 CategoriaBokatas enums
    for item in factura.desglose_categorias:
        assert isinstance(item.categoria, CategoriaBokatas)
    
    print("==================================================================")
    print(f"PIPELINE EXTRACTION SUCCESS: {factura.proveedor} ({factura.numero_factura})")
    print(f"Sede: {factura.sede} | Fecha: {factura.fecha_factura} | Total: €{factura.importe_total:.2f}")
    print("------------------------------------------------------------------")
    print("ITEMIZED LINE BREAKDOWN:")
    for idx, item in enumerate(factura.desglose_categorias, 1):
        print(f"  [{idx}] [{item.categoria.value:<22}] {item.concepto:<38} : €{item.importe_linea:.2f}")
    print("==================================================================")
    print("Arithmetic check: €{:.2f} calculated == €{:.2f} ticket total. 0.00 discrepancy.".format(total_lineas, factura.importe_total))
    return factura

if __name__ == "__main__":
    test_pipeline_validation()

# 💳 Sistema de Gestión de Cuentas Bancarias (Consola · Python)

## 👤 Autor
**Samuel Calderón Soto**

---

## 📝 Descripción
Este proyecto es un **Sistema de Gestión de Cuentas Bancarias** desarrollado en **Python**, que permite simular operaciones bancarias básicas desde consola.  

El sistema incluye:
- 🆕 **Creación de cuentas** con datos personales y productos asociados.  
- 💰 **Depósitos y retiros** de dinero.  
- 🏦 **Solicitud y pago de créditos** con evaluación por **Relación Cuota–Ingresos (RCI)**.  
- 📈 **Gestión de portafolio** (Cuenta Ahorros, Corriente, CDT).  
- 📜 **Historial de movimientos** por producto.  
- ❌ **Cancelación de productos** (con validaciones de saldo).  

Toda la información se almacena en un archivo **JSON persistente** (`data/cuentasBancarias.json`).

---

## 🧰 Stack Tecnológico
- **Lenguaje:** Python 3.x  
- **Entorno:** Consola / Terminal  

### Librerías estándar
- `os` → limpieza de consola  
- `json` → persistencia de datos  
- `time`, `datetime` → gestión de fechas y pausas  

### Librerías externas
*(No requiere ninguna actualmente, pero se puede integrar `colorama` para añadir colores en consola).*

---

## ✅ Requerimientos
- **Python 3.8 o superior.**  

Clonar el repositorio y ejecutar el archivo principal:
```bash
python main.py
```

## 🗂️ Estructura de Archivos
```
/proyecto-banco
│
├── main.py               # Punto de entrada, lanza el menú principal
└── modules/
│   └── corefiles.py          # Manejo de persistencia en JSON (lectura, escritura, actualización, borrado)
│   └── menu.py               # Lógica de menús (principal, clientes, saldos, créditos, portafolio)
│   └── operaciones.py        # Funciones principales (crear cuenta, depositar, crédito, retirar, cancelar, pagar cuota)
│   └── utilidades.py         # Funciones auxiliares (limpiar consola, pausas)
└── data/
    └── cuentasBancarias.json   # Base de datos persistente en formato JSON

```

## 📦 Módulos y Responsabilidades
- *main.py*
    Llama a **menu.menuPrincipal()** y arranca el sistema  

- *corefiles.py*
    - Lectura y escritura de archivos JSON.  
    - Inicialización de estructura base (**cuentasBancarias**).  
    - Funciones de actualización y eliminación dentro del JSON

- *menu.py*
    - Contiene los menús interactivos para el usuario.  
    - Incluye menús anidados: principal, clientes, saldos, créditos y portafolio  

- *operaciones.py*
    - Funciones de negocio:
        - **crear_cuenta()**  
        - **depositar()**  
        - **solicitarCredito()** (con validación RCI)  
        - **retirar()**  
        - **pagoCuota()**  
        - **cancelarCuenta()**  
    - Todas actualizan el archivo JSON y mantienen historial

- *utilidades.py*
    - Limpieza de pantalla.  
    - Pausa temporal entre operaciones  

## 📊 Diagrama general del sistema

```
                 ┌──────────────────────────┐
                 │     main.py (Inicio)     │
                 └───────────┬──────────────┘
                             │
                             ▼
                 ┌──────────────────────────┐
                 │   menuPrincipal()        │
                 │    (menu.py)             │
                 └───────────┬──────────────┘
                             │
        ┌────────────────────┼─────────────────────┐
        ▼                    ▼                     ▼
  ┌───────────────┐   ┌───────────────┐     ┌───────────────┐
  │ operaciones   │   │ menuClientes() │     │ utilidades.py │
  │ (crear, dep...)│   │ (saldos, etc.)│     │ (pausas/limp.)│
  └───────────────┘   └───────────────┘     └───────────────┘
                             │
                             ▼
                       ┌───────────────┐
                       │ corefiles.py  │
                       │ (JSON persist.)│
                       └───────────────┘
```

## 🧭 Menú Principal (flujo de uso)
```
=== Menú Principal ===

1. Crear cuenta   ─────────► operaciones.crear_cuenta()
2. Depositar      ─────────► operaciones.depositar()
3. Solicitar crédito ──────► operaciones.solicitarCredito()
4. Retirar dinero ─────────► operaciones.retirar()
5. Pago cuota     ─────────► operaciones.pagoCuota()
6. Cancelar cuenta────────► operaciones.cancelarCuenta()
7. Estadísticas   ─────────► menuClientes()
0. Salir          ─────────► utilidades.Limpiar_consola()

```

Cada opción invoca una función en **operaciones.py** y registra movimientos en el historial del producto.

## 👥 Menú Clientes
```
=== Menú Clientes ===

1. Datos Cliente   ───────► (pendiente de implementación)
2. Saldos          ───────► menuSaldos()
3. Créditos        ───────► menuCreditos()
4. Inversiones     ───────► (pendiente de implementación)
0. Salir           ───────► utilidades.Limpiar_consola()

```

## 💰 Menú de Saldos
```
=== Menú de Saldos ===

1. Cuenta de Ahorros ─────► producto = "Cuenta de Ahorros"
2. Cuenta Corriente  ─────► producto = "Cuenta Corriente"
0. Salir             ─────► utilidades.Limpiar_consola()

```

## 🏦 Menú de Créditos
```
=== Menú de Créditos ===

1. Crédito Libre Inversión ──► producto = "Crédito Libre Inversión"
2. Crédito Vivienda         ──► producto = "Crédito Vivienda"
3. Crédito Compra Auto      ──► producto = "Crédito Compra Automóvil"
0. Salir                    ──► utilidades.Limpiar_consola()

```

## 📈 Menú de Portafolio
```
=== Menú del Portafolio ===

1. Cuenta Ahorros  ─────► producto = "Cuenta Ahorros"
2. Cuenta Corriente─────► producto = "Cuenta Corriente"
3. CDT              ─────► producto = "CDT"
0. Salir            ─────► utilidades.Limpiar_consola()

```
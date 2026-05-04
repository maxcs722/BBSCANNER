# ⚡ BBScanner AI Hunter

Herramienta avanzada de **reconocimiento y análisis de superficie de ataque** para bug bounty y pentesting.

Combina escaneo de red, detección de vulnerabilidades, fuzzing y análisis inteligente en una interfaz moderna en tiempo real.

---

## 🚀 Características

* 🔍 Escaneo de puertos con Nmap
* 🚨 Detección de vulnerabilidades con Nuclei
* 🧠 Fuzzing automático con ffuf
* 🤖 Clasificación inteligente de endpoints (AI Hunter)
* ⚡ WebSocket en tiempo real (sin polling)
* 📊 Interfaz moderna estilo dashboard
* 📄 Exportación de reportes (PDF)

---

## 🧠 Tecnologías utilizadas

* Python 3
* Flask
* Flask-SocketIO
* Nmap
* Nuclei
* ffuf

---

## 📦 Instalación

### 1. Clonar repositorio

```bash
git clone https://github.com/tuusuario/bbscanner.git
cd bbscanner
```

---

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 4. Instalar herramientas externas

```bash
sudo apt install nmap ffuf -y
```

Instalar Nuclei:

```bash
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
```

Actualizar templates:

```bash
nuclei -update-templates
```

---

## ▶️ Uso

```bash
python app.py
```

Abrir en navegador:

```
http://127.0.0.1:5000
```

---

## 🧪 Flujo de trabajo

1. Introducir dominio objetivo
2. Escaneo automático:

   * Resolución DNS
   * Nmap
   * Headers
   * Nuclei
   * Fuzzing
3. Visualización en tiempo real
4. Análisis de endpoints críticos

---

## 📊 Ejemplo de hallazgos

* `/admin` → Panel de administración
* `/api/v1` → Endpoint API
* `/.env` → Archivo sensible (CRÍTICO)
* `/backup.zip` → Backup expuesto

---

## ⚠️ Disclaimer

Esta herramienta está diseñada únicamente para:

* Programas de bug bounty
* Entornos autorizados
* Laboratorios de seguridad

El uso no autorizado puede ser ilegal.

---

## 🧠 Roadmap

* [ ] Multi-target scanning
* [ ] Autenticación (SaaS)
* [ ] Base de datos de resultados
* [ ] Exportación avanzada
* [ ] Crawling inteligente
* [ ] Detección de parámetros

---

## 👨‍💻 Autor

Proyecto desarrollado como herramienta de aprendizaje y uso en seguridad ofensiva.

---

## ⭐ Contribuciones

Pull requests bienvenidos.
Ideas y mejoras son aceptadas.

---

## 📜 Licencia

MIT License

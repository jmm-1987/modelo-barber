# Funcionalidad: Subir Imágenes para Servicios y Peluqueros

## 🎯 Nueva Funcionalidad Implementada

Se ha agregado la capacidad de **subir imágenes desde el dispositivo local** para servicios y peluqueros en la página de configuración.

## ✅ Características Implementadas

### **Backend - Endpoints Nuevos**

#### 1. **Subir Imagen de Servicio**
- **Endpoint**: `/subir_imagen_servicio`
- **Método**: `POST`
- **Funcionalidad**: Sube una imagen para un servicio específico
- **Validaciones**: 
  - ✅ Tipos de archivo permitidos: `png`, `jpg`, `jpeg`, `gif`, `webp`
  - ✅ Nombres únicos para evitar conflictos
  - ✅ Almacenamiento en `static/uploads/`

#### 2. **Subir Imagen de Peluquero**
- **Endpoint**: `/subir_imagen_peluquero`
- **Método**: `POST`
- **Funcionalidad**: Sube una imagen para un peluquero específico
- **Validaciones**: Mismas que servicios

#### 3. **Eliminar Imagen de Servicio**
- **Endpoint**: `/eliminar_imagen_servicio`
- **Método**: `POST`
- **Funcionalidad**: Elimina la imagen de un servicio
- **Características**: 
  - ✅ Elimina archivo físico del servidor
  - ✅ Actualiza base de datos

#### 4. **Eliminar Imagen de Peluquero**
- **Endpoint**: `/eliminar_imagen_peluquero`
- **Método**: `POST`
- **Funcionalidad**: Elimina la imagen de un peluquero
- **Características**: Mismas que servicios

### **Frontend - Interfaz Mejorada**

#### **Sección de Servicios**
- ✅ **Botón "📁 Seleccionar Imagen"**: Abre selector de archivos
- ✅ **Vista previa en tiempo real**: Muestra la imagen seleccionada
- ✅ **Botón "🗑️ Eliminar"**: Elimina la imagen actual
- ✅ **Placeholder**: Muestra logo cuando no hay imagen

#### **Características de la Interfaz**
- 🎨 **Diseño moderno**: Botones con gradientes y efectos hover
- 📱 **Responsive**: Funciona en móvil y desktop
- ⚡ **Feedback inmediato**: Mensajes de éxito/error
- 🔄 **Actualización automática**: La vista previa se actualiza al subir

## 🎨 Estilos CSS Agregados

```css
/* Contenedor de subida de imágenes */
.imagen-upload-container {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 10px;
}

/* Botón verde para subir */
.btn-subir-imagen {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

/* Botón rojo para eliminar */
.btn-eliminar-imagen {
  background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

/* Vista previa de imagen */
.imagen-preview {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100px;
  border: 2px dashed #ddd;
  border-radius: 8px;
  background: #f8f9fa;
}
```

## 🔧 Funciones JavaScript Agregadas

### **Para Servicios**
```javascript
// Subir imagen de servicio
async function subirImagenServicio(input, servicioId) {
  // Maneja la subida de archivos
  // Actualiza vista previa
  // Muestra mensajes de feedback
}

// Eliminar imagen de servicio
async function eliminarImagenServicio(servicioId) {
  // Elimina imagen del servidor
  // Actualiza vista previa
  // Maneja servicios nuevos vs existentes
}
```

## 📁 Estructura de Archivos

### **Directorio de Uploads**
```
static/
├── uploads/           # Nuevo directorio
│   ├── servicio_1_abc123.png
│   ├── servicio_2_def456.jpg
│   ├── peluquero_1_ghi789.png
│   └── peluquero_2_jkl012.webp
├── logo.png          # Placeholder por defecto
└── ... (otros archivos)
```

### **Nomenclatura de Archivos**
- **Servicios**: `servicio_{id}_{hash}.{extension}`
- **Peluqueros**: `peluquero_{id}_{hash}.{extension}`
- **Ejemplo**: `servicio_1_a1b2c3d4.png`

## 🔒 Seguridad Implementada

### **Validaciones de Archivo**
- ✅ **Tipos permitidos**: Solo imágenes (`png`, `jpg`, `jpeg`, `gif`, `webp`)
- ✅ **Nombres seguros**: `secure_filename()` para evitar inyección
- ✅ **Nombres únicos**: UUID para evitar conflictos
- ✅ **Tamaño limitado**: Configurable en Flask

### **Manejo de Errores**
- ✅ **Archivo no seleccionado**: Mensaje informativo
- ✅ **Tipo no permitido**: Lista de tipos válidos
- ✅ **Error de subida**: Mensaje detallado
- ✅ **Error de eliminación**: Feedback apropiado

## 🎯 Cómo Usar

### **Para Administradores**

1. **Ir a Configuración**: `http://localhost:5000/configuracion`

2. **Sección Servicios**:
   - Hacer clic en "📁 Seleccionar Imagen"
   - Elegir archivo de imagen
   - Ver vista previa automática
   - Usar "🗑️ Eliminar" si es necesario

3. **Sección Peluqueros** (próximamente):
   - Misma funcionalidad que servicios
   - Imágenes de perfil de peluqueros

### **Flujo de Trabajo**
```
Seleccionar Archivo → Validar → Subir → Actualizar Vista → Feedback
```

## 🚀 Beneficios

### **Para el Negocio**
1. **Personalización**: Cada servicio puede tener su imagen única
2. **Profesionalismo**: Imágenes de alta calidad para servicios
3. **Identidad visual**: Logos y fotos de peluqueros
4. **Marketing**: Imágenes atractivas para clientes

### **Para los Clientes**
1. **Visualización**: Ver imágenes de servicios antes de reservar
2. **Reconocimiento**: Identificar peluqueros por foto
3. **Confianza**: Imágenes profesionales generan confianza

### **Para Administradores**
1. **Facilidad**: Subida simple desde dispositivo local
2. **Control**: Eliminar imágenes cuando sea necesario
3. **Feedback**: Mensajes claros de éxito/error
4. **Organización**: Archivos automáticamente organizados

## 🔄 Próximos Pasos

### **Funcionalidades Pendientes**
- [ ] **Imágenes para Peluqueros**: Implementar en sección peluqueros
- [ ] **Redimensionamiento**: Optimizar tamaño de imágenes
- [ ] **Compresión**: Reducir tamaño de archivos
- [ ] **Múltiples formatos**: Soporte para más tipos de imagen
- [ ] **Galería**: Vista de todas las imágenes subidas

### **Mejoras Futuras**
- [ ] **Drag & Drop**: Arrastrar archivos para subir
- [ ] **Vista previa mejorada**: Zoom y rotación
- [ ] **Categorías**: Organizar imágenes por tipo
- [ ] **Backup**: Sistema de respaldo de imágenes

¡La funcionalidad está lista para usar! 🎉 
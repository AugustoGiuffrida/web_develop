# Flask

## API
Una API (Application Programming Interface) es un conjunto de reglas y definiciones que permiten que dos sistemas o aplicaciones se comuniquen entre sí.

## API-RESTS
REST: arquitectura de software para aplicaciones web.

1. Cliente-Servidor: El cliente está separado del servidor. 
2. Sin estado: No se almacena la información del cliente entre las solicitudes. Cada una de ellas es independiente y está desconectada del resto. 
3. Cache: Datos que pueden almacenarse en caché y optimizan las interacciones entre el cliente y el servidor.
4. HTTP: Protocolo por el cual el cliente accede a los recursos.

## Recursos
Un recurso es cualquier entidad que la API maneja y expone a través de sus endpoints.

- Cada recurso tiene una URL única que lo identifique. Los servicios web RESTful se basan en la idea de que todo en la aplicación es un recurso, y que cada recurso puede ser identificado de forma única mediante una URL.
- El cliente puede manipular los recursos a través de la representación que recibe, ya que esta contiene suficiente información para permitirlo. 
- Una colección de todos los recursos debe tener asignada una URL.

## MÉTODOS DE REQUEST
- GET para obtener un recurso del servidor 
- POST para crear un recurso del servidor 
- PUT para actualizar un recurso del servidor 
- DELETE para eliminar un recurso del servidor

## FLASK RESTful
Módulo que brinda soporte para la construcción rápida de APIS REST. Flask-RESTful se encarga de manejar las solicitudes HTTP (GET, POST, PUT, DELETE, etc.) y generar respuestas en formato JSON, XML u otros formatos.

## Recursos Flask-RESTful
Los recursos son clases que definen la lógica de negocio para cada solicitud HTTP que se maneja en una API RESTful. Los recursos se encargan de procesar las solicitudes y generar las respuestas correspondientes.

## ORM (mapeo objeto-relacional)
Permite que en lugar de realizar un código en sql para acceder y manipular a los datos, se trabaja con objetos de programación que representan los datos en la DB (Traduce las operaciones entre los objetos de programación a instrucciones en sql).

## Flask-SQLAlchemy
Extensión de Flask que permite una integración facil de la biblioteca SQLAlchemy a Flask. Es una herramienta de mapeo objeto-relacional (ORM).

## Paginacion
Técnica usada en APIs para dividir grandes conjuntos de datos en páginas más pequeñas, facilitando su consumo y mejorando el rendimiento del servidor y la aplicación cliente.

- Paginación con Offset: Este método usa los parámetros limit y offset para obtener un subconjunto de registros.
- Paginación basada en Keyset: Se basa en una clave única y ordenada (como id o created_at).

## JWT
- Es un estándar abierto de internet para la creación de tokens de acceso, definiendo así un formato seguro para transmitir información de manera digital entre partes. Son tokens basados en JSON.
- Evita la necesidad de guardar datos se sesión del lado del servidor en las API.
- Permite que un usuario se autentique y acceda a recursos o servicios protegidos.

### JWT - LOGIN
Cómo sería un proceso de login:
- El cliente (front) envía las credenciales.
- El servidor genera un JWT y se lo devuelve al cliente
- El cliente guarda ese token para utilizarlo en las diferentes consultas.

### JWT - ESTRUCTURA
- Cabecera: describe el tipo de token y el algoritmo de cifrado utilizado para firmar y verificar la integridad del token.
- Contenido o payload: contiene la información del usuario o la entidad que está siendo autenticada o autorizada.
- Firma o Signature: es un hash criptográfico generado a partir de la combinación de la primera y la segunda sección, y se utiliza para verificar la integridad del token.

### JWT - ACCESO AL RECURSO
- El cliente envía con su solicitud (GET, POST, etc) el token.
- La API verifica que dicho token no está vencido y que es válido.
- La API verifica que el rol del cliente tiene permisos para acceder al recurso que está intentando consumir.
- El servidor responde con el recurso solicitado.

# Angular

## Enrutamiento
Permite navegar entre diferentes vistas de la aplicación sin necesidad de recargar la página. Se gestiona con el módulo de enrutamiento (`RouterModule`) y funciona a través de URLs definidas en la configuración de rutas.

Angular es una SPA (Single Page Application), lo que significa que carga una sola página HTML (index.html) y usa el enrutador para mostrar diferentes vistas sin necesidad de recargar la página completa.

En lugar de que el navegador haga una petición al servidor cada vez que cambias de vista, Angular cambia los componentes dinámicamente en el `<router-outlet>`. Esto mejora el rendimiento y la experiencia del usuario porque la navegación es mucho más rápida.

## Componentes
Los componentes son los principales bloques de construcción de aplicaciones en angular. Cada componente representa una parte de una página web más grande. Organizar una aplicación en componentes ayuda a proporcionar estructura a su proyecto, separando el código en partes que son fáciles de mantener y crecer con el tiempo.

Cada componente consta de:
- Un archivo HTML (Template: fragmento de la interfaz de usuario, no incluye elementos como `<html>` o `<body>`)
- Un archivo ts (define el comportamiento)
- Un archivo CSS.
- Un archivo spec.ts (de testing)

## Observables
Un observable en Angular es un objeto que emite datos de forma asíncrona y que se usa para manejar eventos.

## Suscribe
El método subscribe es la forma de suscribirse a un `Observable` para recibir los valores que emite. Cuando te suscribes, defines cómo se manejarán:

  - `next`:
    Callback que se ejecuta cada vez que el Observable emite un nuevo valor. Aquí procesas los datos que llegan.

  - `error`:
    Callback que se ejecuta si ocurre algún error en el flujo de datos. Esto te permite capturar y manejar errores, como problemas de red o errores del servidor.

  - `complete`:
    Callback que se ejecuta cuando el Observable ha terminado de emitir valores y no se esperan más emisiones. No es obligatorio pero puede ser útil para liberar recursos o ejecutar lógica final.

## OnInit
Es una interfaz importada desde @angular/core que Angular utiliza para identificar componentes que desean realizar operaciones de inicialización.    

## ngOnInit()
Metodo que se llama una vez que Angular ha inicializado las propiedades de entrada (inputs) del componente

## async	
Convierte automáticamente una función en una que devuelve una promesa.

## await	
Pausa la ejecución de la función hasta que la promesa se resuelva. Solo se puede usar dentro de async.

## Promesas 
son objetos en JavaScript/TypeScript que representan una operación asíncrona que puede estar en uno de estos tres estados:

  - Pendiente (pending) → Aún no se ha completado ni rechazado.
  - Resuelta (fulfilled) → Se completó exitosamente y devuelve un resultado.
  - Rechazada (rejected) → Ocurrió un error.

## FormGroup
Representar el formulario en su conjunto. Este objeto agrupa varios controles (campos) y gestiona su estado

## FormBuilder
FormBuilder es una clase que Angular proporciona para facilitar la creación y configuración de formularios reactivos.
Permite construir un FormGroup de manera más sencilla y legible, en lugar de tener que instanciar manualmente cada control.

## Señales
Las señales (signals) son una forma de gestionar el estado reactivo en las aplicaciones. Permiten la lectura y actualización de datos. Angular detecta automáticamente cuándo cambia el valor de una señal y actualiza los componentes que la usan, optimizando el rendimiento.

```ts
import { signal } from '@angular/core';

// Definir una señal con un valor inicial
const firstName = signal('Morgan');

// Leer su valor llamándola como una función
console.log(firstName()); // Output: Morgan

// Actualizar una señal
firstName.set('Jaime');
console.log(firstName()); // Output: Jaime

// Modificar el valor actual
firstName.update(name => name.toUpperCase());
console.log(firstName()); // Output: JAIME
```

## Directivas
Las directivas son clases que añaden comportamiento adicional a los elementos de la aplicacion.

### Directrices de atributo
Cambie la apariencia o el comportamiento de los elementos DOM.

| **Directivas comunes** | **Detalles** |
|----------------------|----------------------------------------------|
| `NgClass`           | Añade y elimina un conjunto de clases de CSS. |
| `NgStyle`           | Añade y elimina un conjunto de estilos HTML.  |
| `NgModel`           | Añade la unión de datos bidireccionales a un elemento de formulario HTML (Vincula un input con una variable en TypeScript.). |

### Directrices estructurales
Las directivas estructurales son responsables de la disposición HTML. Forman o remodelan la estructura del DOM, típicamente añadiendo, eliminando y manipulando los elementos. Siempre llevan el prefijo * porque afectan la estructura del HTML.

| **Directivas comunes** | **Detalles** |
|--------------------------------|------------------------------------------------|
| `NgIf`                         | Muestra u oculta un elemento dependiendo de una condición. |
| `NgFor`                        | Recorre un array y genera elementos en el DOM. |
| `NgSwitch`                     | Un conjunto de directivas que cambian entre puntos de vista alternativos. |


## DOM (Document Object Model) 
Es una representación estructurada de una página web en forma de árbol. Cuando un navegador carga una página HTML, crea un modelo jerárquico que permite a los lenguajes como JavaScript y TypeScript manipular los elementos de la página de manera dinámica.

## Servicios
Son piezas de código reutilizables que se pueden inyectar.

Los servicios se componen de lo siguiente:

- Decorador de TypeScript que declara la clase como un servicio Angular vía @Injectable y permite definir qué parte de la aplicación puede acceder al servicio a través de la propiedad providedIn (Se usa el parametro `root` para crear una unica instancia en la app y `any` para inyectar el servicio en el componente mas cercano).
- Una clase de TypeScript que define el código que será accesible cuando se inyecta el servicio.

```ts
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root' // Define el alcance del servicio
})
export class EjemploService {
  private mensaje = 'Hola desde el servicio';

  getMensaje(): string {
    return this.mensaje;
  }
}
```

## Inyección de dependencia
Cuando necesita compartir lógica entre componentes, Angular utiliza el patrón de diseño de la inyección de dependencia, 
el cual crea un servicio que le permite inyectar código en los componentes que lo requieran mientras lo gestiona desde una sola fuente
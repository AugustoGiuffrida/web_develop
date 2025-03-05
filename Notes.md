# Angular

## Enrutamiento
Permite navegar entre diferentes vistas de la aplicación sin necesidad de recargar la página. Se gestiona con el módulo de enrutamiento (`RouterModule`) y funciona a través de URLs definidas en la configuración de rutas.

Angular es una SPA (Single Page Application), lo que significa que carga una sola página HTML (index.html) y usa el enrutador para mostrar diferentes vistas sin necesidad de recargar la página completa.

En lugar de que el navegador haga una petición al servidor cada vez que cambias de vista, Angular cambia los componentes dinámicamente en el <router-outlet>. Esto mejora el rendimiento y la experiencia del usuario porque la navegación es mucho más rápida.

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
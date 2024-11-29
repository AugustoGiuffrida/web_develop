import { trigger, style, animate, transition } from '@angular/animations';

export const slideInOutAnimation = trigger('slideInOut', [
  transition(':enter', [ // Animación al entrar
    style({ transform: 'translateX(100%)', opacity: 0 }),
    animate('300ms ease-in', style({ transform: 'translateX(0)', opacity: 1 }))
  ]),
  transition(':leave', [ // Animación al salir
    animate('300ms ease-in', style({ transform: 'translateX(-100%)', opacity: 0 }))
  ])
]);

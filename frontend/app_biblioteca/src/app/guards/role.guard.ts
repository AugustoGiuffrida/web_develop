import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { jwtDecode } from 'jwt-decode';

export const roleGuard: CanActivateFn = (route, state) => {
  const router: Router = inject(Router);
  const token = localStorage.getItem('token');

  if (token) {
    try {
      const decoded: any = jwtDecode(token);
      console.log('Decoded Token:', decoded);  // Verifica el contenido del token

      // Verifica si el rol es 'admin' o 'librarian'
      if (decoded && (decoded.rol === 'admin' || decoded.rol === 'librarian')) {
        return true;
      } else {
        console.warn('Access denied: role not authorized');
      }
    } catch (error) {
      console.error('Token decoding failed:', error);
    }
  } else {
    console.warn('Access denied: no token found');
  }

  router.navigateByUrl('home'); // Redirige si no cumple las condiciones
  return false;
};

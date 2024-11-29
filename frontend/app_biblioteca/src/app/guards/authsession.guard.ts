import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';

export const authsessionGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const token = localStorage.getItem('token');
  
  if (!token) {
    router.navigateByUrl('/home').then(() => {
      console.log("Redirigido a la página de inicio debido a la falta de autenticación.");
    });
    return false;
  }
  
  return true;
};

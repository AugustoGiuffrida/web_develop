import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-star',
  styles: ``,
  template: `
  {{ rating.toFixed(1) }}
  <i *ngFor="let i of [].constructor(getStars(rating).fullStars)" class="bi bi-star-fill" style="color: #17a2b8;"></i>
  <i *ngIf="getStars(rating).halfStars" class="bi bi-star-half" style="color: #17a2b8;"></i>
  <i *ngFor="let i of [].constructor(getStars(rating).emptyStars)" class="bi bi-star" style="color: lightgray;"></i>
  `,
})
export class StarComponent {
  @Input() rating: number = 0;

  getStars(rating: number) {
    const fullStars = Math.floor(rating);
    const halfStars = rating % 1 >= 0.5 ? 1 : 0;
    const emptyStars = 5 - fullStars - halfStars;
    return { fullStars, halfStars, emptyStars };
  }
}

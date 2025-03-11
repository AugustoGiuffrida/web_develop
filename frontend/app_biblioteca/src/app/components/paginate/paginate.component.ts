import { Component, EventEmitter, Input, Output, OnChanges, SimpleChanges } from '@angular/core';
//OnChanges y SimpleChanges: se utilizan para reaccionar a cambios en las propiedades de entrada

@Component({
  selector: 'app-paginate',
  templateUrl: './paginate.component.html',
  styleUrls: ['./paginate.component.css'] 
})
export class PaginateComponent implements OnChanges { // interceptar cambios en las propiedades de entrada
  @Input() page: number = 1; //página actual
  @Input() pages: number = 1;//número total de páginas
  @Output() pageChange = new EventEmitter<number>();
  
  ngOnChanges(changes: SimpleChanges) { //se ejecuta cuando una propiedad de entrada cambia
    if (changes['pages'] && changes['pages'].currentValue) { //verificar cambios en la propiedad pages
      this.pages = changes['pages'].currentValue;
    }
  }

  get range(): number[] {
    const rangeSize = 5;
    const halfRange = Math.floor(rangeSize / 2);

    let start = Math.max(1, this.page - halfRange);
    let end = Math.min(this.pages, this.page + halfRange);

    if (end - start + 1 < rangeSize) {
      if (start === 1) {
        end = Math.min(start + rangeSize - 1, this.pages);
      } else if (end === this.pages) {
        start = Math.max(end - rangeSize + 1, 1);
      }
    }

    return Array.from({ length: end - start + 1 }, (_, i) => start + i);
  }

  goToPage(pageNumber: number) { //Cambiar la página actual
    if (pageNumber >= 1 && pageNumber <= this.pages) {
        this.page = pageNumber;
        this.pageChange.emit(pageNumber); 
    }
  }
}



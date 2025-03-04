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

  get range(): number[] { //arreglo de números que representa las páginas
    return Array.from({ length: this.pages }, (_, i) => i + 1);
  }

  goToPage(pageNumber: number) { //Cambiar la página actual
    if (pageNumber >= 1 && pageNumber <= this.pages) {
        this.page = pageNumber;
        this.pageChange.emit(pageNumber); 
    }
  }
}



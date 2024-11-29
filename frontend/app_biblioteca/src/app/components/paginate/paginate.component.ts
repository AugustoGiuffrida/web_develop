import { Component, EventEmitter, Input, Output, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-paginate',
  templateUrl: './paginate.component.html',
  styleUrls: ['./paginate.component.css'] 
})
export class PaginateComponent implements OnChanges {
  @Input() page: number = 1;
  @Input() pages: number = 1;
  @Output() pageChange = new EventEmitter<number>();
  
  ngOnChanges(changes: SimpleChanges) {
    if (changes['pages'] && changes['pages'].currentValue) {
      this.pages = changes['pages'].currentValue;
    }
  }

  get range(): number[] {
    return Array.from({ length: this.pages }, (_, i) => i + 1);
  }

  goToPage(pageNumber: number) {
    if (pageNumber >= 1 && pageNumber <= this.pages) {
        this.page = pageNumber;
        this.pageChange.emit(pageNumber); 
    }
  }
}



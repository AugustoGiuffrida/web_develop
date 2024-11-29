import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LibrarianRentsComponent } from './librarian-rents.component';

describe('LibrarianRentsComponent', () => {
  let component: LibrarianRentsComponent;
  let fixture: ComponentFixture<LibrarianRentsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [LibrarianRentsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LibrarianRentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

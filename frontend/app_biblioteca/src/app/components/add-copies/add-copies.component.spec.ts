import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddCopiesComponent } from './add-copies.component';

describe('AddCopiesComponent', () => {
  let component: AddCopiesComponent;
  let fixture: ComponentFixture<AddCopiesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AddCopiesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddCopiesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

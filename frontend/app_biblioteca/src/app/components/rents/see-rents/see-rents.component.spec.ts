import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeeRentsComponent } from './see-rents.component';

describe('SeeRentsComponent', () => {
  let component: SeeRentsComponent;
  let fixture: ComponentFixture<SeeRentsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SeeRentsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SeeRentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

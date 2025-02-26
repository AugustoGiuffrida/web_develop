import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeeNotificationsComponent } from './see-notifications.component';

describe('SeeNotificationsComponent', () => {
  let component: SeeNotificationsComponent;
  let fixture: ComponentFixture<SeeNotificationsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SeeNotificationsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SeeNotificationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

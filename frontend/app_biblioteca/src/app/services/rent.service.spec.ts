import { TestBed } from '@angular/core/testing';

import { RentService } from '../services/rent.service'; // Ruta correcta del servicio

describe('RentService', () => {
  let service: RentService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RentService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

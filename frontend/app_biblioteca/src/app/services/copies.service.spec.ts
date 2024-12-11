import { TestBed } from '@angular/core/testing';

import { CopiesService } from './copies.service';

describe('CopiesService', () => {
  let service: CopiesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CopiesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

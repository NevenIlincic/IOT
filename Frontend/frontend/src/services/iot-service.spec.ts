import { TestBed } from '@angular/core/testing';

import { IotService } from './iot-service';

describe('IotService', () => {
  let service: IotService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(IotService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

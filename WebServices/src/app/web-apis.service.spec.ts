import { TestBed } from '@angular/core/testing';

import { WebApisService } from './web-apis.service';

describe('WebApisService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: WebApisService = TestBed.get(WebApisService);
    expect(service).toBeTruthy();
  });
});

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageCamerasComponent } from './manage-cameras.component';

describe('ManageCamerasComponent', () => {
  let component: ManageCamerasComponent;
  let fixture: ComponentFixture<ManageCamerasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageCamerasComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ManageCamerasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

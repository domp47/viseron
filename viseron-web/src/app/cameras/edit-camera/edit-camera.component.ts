import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BaseEditComponent } from 'src/app/base-edit.component';
import { CameraService } from 'src/app/services/camera/camera.service';
import { Camera } from 'src/models/camera.model';

@Component({
  selector: 'app-edit-camera',
  templateUrl: './edit-camera.component.html',
  styleUrls: ['./edit-camera.component.scss']
})
export class EditCameraComponent extends BaseEditComponent implements OnInit {

  camera: Camera | undefined;

  constructor(route: ActivatedRoute, private cameraService: CameraService) { 
    super(route);
  }

  
  override ngOnInit(): void {
    console.log("hello");
    
    super.ngOnInit();
  }

  getItem(id: number) {
    this.cameraService.getCamera(id, {fields: "*"}).subscribe((data: Camera) => {
      this.camera = data;
    });
  }
}

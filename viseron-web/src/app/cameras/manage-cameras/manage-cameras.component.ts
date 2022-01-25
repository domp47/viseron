import { Component, OnInit } from '@angular/core';
import { CameraService } from 'src/app/services/camera/camera.service';
import { Camera } from 'src/models/camera.model';

@Component({
  selector: 'app-manage-cameras',
  templateUrl: './manage-cameras.component.html',
  styleUrls: ['./manage-cameras.component.scss']
})
export class ManageCamerasComponent implements OnInit {

  dataSource: Camera[] = [];
  displayedColumns: string[] = ['name', 'source', 'recordings', 'r-enabled', 'o-enabled'];

  constructor(private cameraService: CameraService) { }

  ngOnInit(): void {
    const fields = "id,name,host,port,motion_trigger_recorder,object_enabled"
    this.cameraService.getCameraList({fields: fields}).subscribe((data: any) => {
      this.dataSource = data["results"];
    });
  }

}

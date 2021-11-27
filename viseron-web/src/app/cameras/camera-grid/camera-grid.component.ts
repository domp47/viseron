import { Component, OnInit } from '@angular/core';
import { CameraService } from 'src/app/services/camera/camera.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-camera-grid',
  templateUrl: './camera-grid.component.html',
  styleUrls: ['./camera-grid.component.scss']
})
export class CameraGridComponent implements OnInit {

  desiredWidth = 800; //px
  cameraList: any[] = [];

  constructor(private cameraService: CameraService) { }

  ngOnInit(): void {
    this.cameraService.getCameraList().subscribe(data => {
      for (const camera of data["results"]) {
        if (camera["camera"]["stream"]["width"] > this.desiredWidth) {
          const factor = Math.floor(camera["camera"]["stream"]["width"] / this.desiredWidth);
          const width  = Math.floor(camera["camera"]["stream"]["width"] / factor);
          const height = Math.floor(camera["camera"]["stream"]["height"] / factor);
          
          camera["camera"]["stream"]["url"] = `${environment.backendUrl}/${camera["config"]["camera"]["name_slug"]}/mjpeg-stream?width=${width}&height=${height}`;
        } else {
          camera["camera"]["stream"]["url"] = `${environment.backendUrl}/${camera["config"]["camera"]["name_slug"]}/mjpeg-stream`;
        }
        this.cameraList.push(camera);
      }
    })
  }

  print(event: any) {
    console.log(event);
  }

}

import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-camera-grid',
  templateUrl: './camera-grid.component.html',
  styleUrls: ['./camera-grid.component.scss']
})
export class CameraGridComponent implements OnInit {

  cameraList: any[] = []

  constructor() { 
    for (let index = 0; index < 5; index++) {
      const obj: any = {}
      obj["name"] = "Front";
      obj["host"] = "192.168.2.1";

      this.cameraList.push(obj);
    }
  }

  ngOnInit(): void {
  }

}

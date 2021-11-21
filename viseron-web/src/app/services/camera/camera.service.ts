import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, map, Observable } from 'rxjs';
import { BaseService } from '../base.service';

@Injectable({
  providedIn: 'root'
})
export class CameraService extends BaseService {

  constructor(private http: HttpClient) { 
    super("camera");
  }

  getCameraList(): Observable<any> {
    return this.http.get(this.url).pipe(
      map(data => data),
      catchError(err => this.handleError("Error Getting Camera List", err))
    )
  }
}

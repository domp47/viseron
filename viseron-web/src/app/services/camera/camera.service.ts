import { HttpClient, HttpParams } from '@angular/common/http';
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

  getCameraList(queryParams: any | undefined = undefined): Observable<any> {
    let params = new HttpParams();

    for(const [key, value] of Object.entries(queryParams || {})) {
      params = params.set(key, value as string);
    }

    return this.http.get(this.url, {params: params}).pipe(
      map(data => data),
      catchError(err => this.handleError("Error Getting Camera List", err))
    )
  }

  getCamera(cameraId: number, queryParams: any | undefined = undefined): Observable<any> {
    let params = new HttpParams();

    for(const [key, value] of Object.entries(queryParams || {})) {
      params = params.set(key, value as string);
    }

    return this.http.get(`${this.url}/${cameraId}`, {params: params}).pipe(
      map(data => data),
      catchError(err => this.handleError("Error Getting Camera List", err))
    )
  }
}

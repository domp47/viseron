import { Observable, of } from 'rxjs';
import { environment } from 'src/environments/environment';


export interface ListResponse<T> {
  results: T[];
}

export class BaseService {

    protected url: string;
  
    constructor(route: string) { 
      this.url = environment.backendUrl + "/api/v1/" + route;
    }
  
      handleError(title: string, err: Response | any): Observable<any> {
      console.error(title);
      console.error(err);
      return of();
    }
  }
  
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AboutComponent } from './about/about.component';
import { CameraGridComponent } from './cameras/camera-grid/camera-grid.component';
import { EditCameraComponent } from './cameras/edit-camera/edit-camera.component';
import { ManageCamerasComponent } from './cameras/manage-cameras/manage-cameras.component';
import { HomeComponent } from './home/home.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent
  },
  {
    path: 'about',
    component: AboutComponent
  },
  {
    path: 'cameras',
    component: CameraGridComponent
  },
  {
    path: 'manage-cameras',
    component: ManageCamerasComponent
  },
  {
    path: 'manage-cameras/:id',
    component: EditCameraComponent
  },
  {
    path: '**',
    redirectTo: ''
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

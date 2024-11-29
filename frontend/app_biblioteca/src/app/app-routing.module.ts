import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './page/home/home.component';
import { ErrorPageComponent } from './page/error-page/error-page.component';
import { ConfigurationComponent } from './page/configuration/configuration.component';
import { ForgotPasswordComponent } from './page/forgot-password/forgot-password.component';
import { LibrarianRentsComponent } from './page/librarian-rents/librarian-rents.component';
import { NotificationsComponent } from './page/notifications/notifications.component';
import { ProfileComponent } from './page/profile/profile.component';
import { RegisterComponent } from './page/register/register.component';
import { UsersComponent } from './page/users/users.component';
import {BookDetailsComponent} from './page/book-details/book-details.component';
import { authsessionGuard } from './guards/authsession.guard';
import { roleGuard } from './guards/role.guard';
import { LoginComponent } from './page/login/login.component'; 

const routes: Routes = [
  {path: 'login', component: LoginComponent},
  {path: 'configuration', component: ConfigurationComponent, canActivate: [authsessionGuard]},
  {path: 'error_page', component: ErrorPageComponent},
  {path: 'forgot-password', component: ForgotPasswordComponent},
  {path: 'home', component: HomeComponent},
  {path: 'librarian-rents', component: LibrarianRentsComponent, canActivate: [authsessionGuard, roleGuard]},
  {path: 'profile', component: ProfileComponent},
  {path: 'notifications', component: NotificationsComponent, canActivate: [authsessionGuard, roleGuard]},
  {path: 'register', component: RegisterComponent},
  {path: 'users', component: UsersComponent, canActivate: [authsessionGuard, roleGuard]},
  {path: 'book/:id', component: BookDetailsComponent},

  {path: '', redirectTo: 'home', pathMatch:'full'},
  {path: '**', redirectTo: 'error_page'}  

];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

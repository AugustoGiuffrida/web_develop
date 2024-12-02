import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './page/home/home.component';
import { ErrorPageComponent } from './page/error-page/error-page.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { NotificationsComponent } from './page/notifications/notifications.component';
import { ProfileComponent } from './page/profile/profile.component';
import { RegisterComponent } from './page/register/register.component';
import { UsersComponent } from './page/users/users.component';
import { LibrarianRentsComponent } from './page/librarian-rents/librarian-rents.component';
import { ForgotPasswordComponent } from './page/forgot-password/forgot-password.component';
import { SeeUserComponent } from './components/user/see-user/see-user.component';
import { SeeRentsComponent } from './components/rents/see-rents/see-rents.component';
import { BookComponent } from './components/book/book.component';
import { PaginateComponent } from './components/paginate/paginate.component';
import { NgClass } from '@angular/common';
import { BookDetailsComponent } from './page/book-details/book-details.component';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { LoginComponent } from './page/login/login.component';
import {BookEditComponent} from './page/book-edit/book-edit.component';
import { StarComponent } from './components/star/star.component';
import { ReviewComponent } from './components/review/review.component';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ErrorPageComponent,
    NavbarComponent,
    NotificationsComponent,
    ProfileComponent,
    RegisterComponent,
    UsersComponent,
    LibrarianRentsComponent,
    ForgotPasswordComponent,
    SeeUserComponent,
    SeeRentsComponent,
    PaginateComponent,
    BookComponent,
    BookDetailsComponent,
    LoginComponent,
    StarComponent,
    ReviewComponent,
    BookEditComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    NgClass,
    HttpClientModule
  ],
  providers: [{provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true}],
  bootstrap: [AppComponent],
})
export class AppModule { }


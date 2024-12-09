import { Component,Input } from '@angular/core';
import { StarComponent } from '../star/star.component';
import { UsuariosService } from '../../services/usuarios.service';
import { AuthService } from '../../services/auth.service';
import { ReviewsService } from '../../services/reviews.service';

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrl: './review.component.css'
})
export class ReviewComponent {
  @Input() id!: number;
  @Input() reviewID: number = 0;
  @Input() valoration: number = 0;
  @Input() comment: string = '';
  @Input() self_comment: any = null;
  user: any = null;

  constructor(private usuariosService: UsuariosService, private authService: AuthService, private reviewService: ReviewsService) {}

  ngOnInit() {
    this.usuariosService.getUser(this.id).subscribe(user => {
    this.user = user;
  });
  }

  get isAdmin(): boolean {
    return this.authService.isAdmin();
  }

  getUser(usuarioID: number): void  {
    this.usuariosService.getUserName(usuarioID).subscribe(user => {
      this.user = user;
    })
  }

  getUserImage(user: any) {
    if (!user?.image || user?.image === '') {
      return `https://via.placeholder.com/150?text=${user?.usuario_nombre[0]}${user?.usuario_apellido[0]}`;
    }
    return user?.image;
  }

  deleteComment() {
    this.reviewService.deleteReview(this.reviewID).subscribe({
      next: () => {
        window.location.reload();
      },
      error: (err) => {
        console.error(err);
      }
    })
  }

}
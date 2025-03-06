import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { StarComponent } from '../../components/star/star.component';
import { ReviewComponent } from '../../components/review/review.component';
import { BookService } from '../../services/book.service';
import { ReviewsService } from '../../services/reviews.service';
import { AuthService } from '../../services/auth.service';



@Component({
  selector: 'app-book-details',
  templateUrl: './book-details.component.html',
  styleUrls: ['./book-details.component.css']
})
export class BookDetailsComponent implements OnInit {
  bookId: number | null = null; 
  titulo: string = '';
  image: string = ''; 
  editorial: string = '';
  genero: string = '';
  autores: string = '';
  cantidad: number = 0; 
  rating: number = 0;
  resenas: any[] = [];
  self_comment: any = null;
  userRating: number = 1;
  userReview: string = '';
  errorMessage: string = '';
  

  constructor(
    private route: ActivatedRoute,
    private bookService: BookService,
    private authService: AuthService,
    private reviewService: ReviewsService
  ) {}

  ngOnInit() {
    // Obtén el ID del libro desde la URL
    this.bookId = Number(this.route.snapshot.paramMap.get('id'));
    // Llama a la función para obtener los detalles del libro
    this.getBook(this.bookId);

  }
  get userId(): number {
    return this.authService.UserId;
  }

  get isToken() {
    return this.authService.isAuthenticated();  
  }

  get isUser(): boolean {
    return this.authService.isUser();
  }
  

  setRating(rating: number) {
    this.userRating = rating;
  }

  postReview() {
    if (this.self_comment) {
      this.errorMessage = "Ya has comentado este libro.";
      return;
    }

    const reviewData = {
      libroID: this.bookId,
      usuarioID: this.authService.UserId,
      valoracion: this.userRating,
      comentario: this.userReview,
    };

    this.reviewService.postReview(reviewData).subscribe({
      next: () => window.location.reload(),
      error: (err) => {
        console.error("Error al enviar la reseña:", err);
        this.errorMessage = "No puedes comentar este libro más de una vez.";
      }
    });
  }

  get isLogged() {
    return this.authService.isLoggedIn()
  }

  // Función para obtener los detalles del libro
  getBook(id: number) {
    this.bookService.getBook(id).subscribe((data: any) => {
      this.titulo = data.titulo;
      this.image = data.image;
      this.editorial = data.editorial;
      this.cantidad = data.cantidad;
      this.genero = data.genero;
      this.resenas = data.resenas;
      this.rating = data.rating;
      this.self_comment = data.self_comment;
  
      if (data.autores && data.autores.length > 0) {
        this.autores = data.autores.map((autor: any) => `${autor.autor_nombre} ${autor.autor_apellido}`).join(', ');
      }
    });
  }
  
  trackByResenaId(index: number, resena: any): number {
    return resena.resenaID; 
  }

}

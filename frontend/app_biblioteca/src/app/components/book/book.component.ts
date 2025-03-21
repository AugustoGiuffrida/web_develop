import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { BookService } from '../../services/book.service';
import { AuthService } from '../../services/auth.service';
import { NotificationsService } from '../../services/notifications.service';
import { UsuariosService } from '../../services/usuarios.service';


@Component({
  selector: 'app-book',
  templateUrl: './book.component.html',
  styleUrls: ['./book.component.css']
})
export class BookComponent implements OnInit {
  @Input() id!: number; 
  @Input() title!: string;
  @Input() author!: any;
  @Input() gender: string = '';
  @Input() quantity: number = 0;
  @Input() image!: string;
  @Input() rating: number = 0;
  @Input() available_copies:any[] = [];
  user: any = {};

  // Propiedades para el formulario de edición
  isEditing: boolean = false;
  updatedTitle: string = '';
  updatedAuthor: string = '';
  updatedGender: string = '';
  updatedQuantity: number = 0;


  ngOnInit() { //se ejecuta al iniciar el componente.
    if (this.isUser) {
      this.getUser();
    }
  }

  constructor(
    private router: Router, 
    private bookService: BookService, 
    private authService: AuthService, 
    private notificationService: NotificationsService, 
    private userService: UsuariosService) {}


  get isAdmin(): boolean {
    return this.authService.isAdmin();
  }

  get isLibrarian(): boolean {
    return this.authService.isLibrarian();
  }

  get isUser(): boolean {
    return this.authService.isUser();
  }

  getUser() {
    const userID = this.authService.UserId; //Obtener el ID del usuario
    this.userService.getUser(userID).subscribe({ //Obtengo datos del usuario
      next: (response) => {
        this.user = response;//Guardo respuesta en la propiedad user
      },
      error: (error) => {
        console.log('Error al obtener el usuario:', error);
      }
    })
  }

  get parseAvailable(): string {
    let result: string = '';
    let comma: string = '';
    for (let copy of this.available_copies) {
      result += comma + copy.copiaID;
      comma = ', ';
    }
    return result
  }

  onRentBook() {
    
    const data = {
      "titulo": "Solicitud de préstamo",
      "descripcion": `El usuario ${this.user?.usuario_email} desea alquilar el libro: ${this.title} (UsuarioID: ${this.user?.usuarioID}, libroID: ${this.id}) copias disponibles: ${this.parseAvailable}.`,
      "categoria": "info"
    };
    
    this.notificationService.postNotification(data).subscribe({
      next: (response) => {
        console.log('Renovar solicitud enviada: ', response);
        alert('¡Tu solicitud de préstamo ha sido enviada con éxito!');
      },
      error: (error) => {
        console.error('Error al enviar la solicitud de préstamo:', error);
        alert('Error al enviar la solicitud. Intenta nuevamente.');
      }
    });
  }

  get authors():string {
    let authors = '';
    try {
      authors = this.author.map((autor: any) => `${autor.autor_nombre} ${autor.autor_apellido}`).join(', ');
    } catch (error) {
      console.log(error);
    }
    return authors;
  }
  
  // Método para navegar a la página de detalles del libro
  navigateToBookDetails() {
    this.router.navigate([`/book`, this.id]); 
  }

  navigateToBookEdit() {
    this.router.navigate([`/book-edit`, this.id]); 
  }

  onDeleteBook() {
    this.bookService.deleteBook(this.id).subscribe(() => {
      window.location.reload();
    });
  }

  onEditBook() {
    this.isEditing = true;
    // Guardamos los valores actuales en el formulario
    this.updatedTitle = this.title;
    this.updatedAuthor = this.authors;
    this.updatedGender = this.gender;
    this.updatedQuantity = this.quantity;

  }

  updateBook() {
    const updatedBookData = {
      titulo: this.updatedTitle,
      autor: this.updatedAuthor,
      cantidad: this.updatedQuantity,
      genero: this.updatedGender
    };

    this.bookService.updateBook(this.id, updatedBookData).subscribe(() => {
      console.log('Libro actualizado');
      this.isEditing = false; // Oculta el formulario
    });
  }


}
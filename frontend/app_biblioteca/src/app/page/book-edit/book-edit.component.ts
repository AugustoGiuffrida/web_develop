import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import { AuthorsService } from '../../services/authors.service';
import { BookService } from '../../services/book.service';

@Component({
  selector: 'app-book-edit',
  templateUrl: './book-edit.component.html',
  styleUrls: ['./book-edit.component.css']
})
export class BookEditComponent implements OnInit {

  bookId: number | null = null; 
  titulo: string = '';
  image: string = ''; 
  editorial: string = '';
  genero: string = '';
  autores: string = '';
  libros_autores: string = "";
  new_authors: any[] = [];
  isLoading = false;
  errors: any = {};


  generos = ['Fiction', 'Non-fiction', 'Mystery', 'Science Fiction', 'Fantasy'];
  editBookForm = new FormGroup({
    title: new FormControl(''),
    description: new FormControl(''),
    author: new FormControl(''),
    editorial: new FormControl(''),
    genero: new FormControl(''),
  })

  constructor(
    private AuthorsService: AuthorsService,
    private bookService: BookService,
    private route: ActivatedRoute
  ) {}


  ngOnInit() {
    // Obtén el ID del libro desde la URL
    this.bookId = Number(this.route.snapshot.paramMap.get('id'));
    // Llama a la función para obtener los detalles del libro
    this.getBook(this.bookId);

  }

  parseAuthors(authors: any): string {
    let result = "";
    for (let i = 0; i < this.autores.length; i++) {
      result += authors[i].autor_nombre + " " + authors[i].autor_apellido;
      if (i < this.autores.length - 1) {
        result += ", ";
      }   
    }
    return result;  
  }
 
  repeatedAuthor(test_id: number): boolean {
    for (let id of  this.new_authors) {
      if (id == test_id) {
        return true;
      }
    }
    return false;
  }  

  addAuthor() {
    console.log(this.new_authors);
    const input = this.editBookForm.controls['author'].value;
    const autor_nombre: string = input?.split(' ')[0] || '';
    const autor_apellido: string = input?.split(' ')[1] || '';
    if (!autor_nombre || !autor_apellido) {
      return;
    } else {
      this.AuthorsService.getAuthor_by_fullname(autor_nombre, autor_apellido).subscribe((answer:any) => {
        const id = answer.autores[0].id;
        if (id && !(this.repeatedAuthor(id))) {
          this.new_authors.push(id);
          this.libros_autores += ', ' + answer.autores[0].autor_nombre + ' ' + answer.autores[0].autor_apellido;
          this.editBookForm.controls['author'].setValue('');
          console.log(this.new_authors);
        }
      })      
    }
  }
  
  getAuthors() {
    const query = this.editBookForm.controls['author'].value
    if (typeof query === 'string') {
      this.AuthorsService.getAuthors_by_name_or_lastname(query).subscribe((answer:any) => {
        this.autores = answer.autores;
      })
    } else {
      this.AuthorsService.getAuthors_by_name_or_lastname('').subscribe((answer:any) => {
        this.autores = answer.autores;
      })
    }
  }

  
  getBook(id: number) {
    this.bookService.getBook(id).subscribe((data: any) => {
      console.log(data); 
      this.titulo = data.titulo;
      this.image = data.image;
      this.editorial = data.editorial;
      
      this.genero = data.genero;
      if (Array.isArray(data.authors) && data.authors.length > 0) {
        this.libros_autores = this.parseAuthors(data.authors);
        for (let author of data.authors) {
          this.new_authors.push(author.id);
        }
      } else {
        this.libros_autores = '';
      }
    });
  }
  
  


  uploadImage(event: any): void {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        this.image = reader.result as string;
      };
      reader.readAsDataURL(file);
    }
  }
  

}

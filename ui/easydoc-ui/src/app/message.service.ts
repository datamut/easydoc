import { Injectable } from '@angular/core';

@Injectable()
export class MessageService {

  message: string = null;

  constructor() { }

  show(message: string) {
    this.message = message;
    setTimeout(() => {
      this.message = null;
    }, 10000);
  }

}

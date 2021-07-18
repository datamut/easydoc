import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MessageService } from '../message.service';
import { ApiResponse } from '../models';
import { StatsService } from '../stats.service';

@Component({
  selector: 'app-uploader',
  templateUrl: './uploader.component.html',
  styleUrls: ['./uploader.component.css']
})
export class UploaderComponent implements OnInit {

  @ViewChild('fileInput')
  fileInput: ElementRef;

  selectedFile: File;

  hasData: boolean = false;
  invoiceData: any;

  constructor(
    private http: HttpClient,
    public messageService: MessageService,
    public statsService: StatsService
  ) { }

  ngOnInit() {
  }

  upload() {
    const formData = new FormData();
    formData.append("file", this.selectedFile, this.selectedFile.name);
    this.http.post("http://localhost:8000/extract_invoice", formData).subscribe(res => {
      this.invoiceData = res;
      this.hasData = true;
    });
  }

  onFileSelected(event) {
    this.selectedFile = <File>event.target.files[0];
    if (this.selectedFile.size >= 20971520) {
      this.messageService.show(`The selected file ${this.selectedFile.name} is over 20M, size=${this.selectedFile.size}, please choose a different file`);
      this.fileInput.nativeElement.value = "";
    }
  }

  save() {
    this.http.post<ApiResponse>("http://localhost:8000/invoice", this.invoiceData).subscribe(res => {
      if (res.status === 'success') {
        this.messageService.show("Invoice saved");
        if(!this.invoiceData.info.amount_due) {
          this.statsService.updateDailyExpense();
        }
      } else {
        this.messageService.show("Failed to save the invoice");
      }
    });
  }
}

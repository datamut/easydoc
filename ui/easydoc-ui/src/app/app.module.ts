import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';


import { AppComponent } from './app.component';
import { UploaderComponent } from './uploader/uploader.component';
import { ChartsComponent } from './charts/charts.component';
import { MessageComponent } from './message/message.component';
import { MessageService } from './message.service';
import { StatsService } from './stats.service';

@NgModule({
  declarations: [
    AppComponent,
    UploaderComponent,
    ChartsComponent,
    MessageComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule
  ],
  providers: [MessageService, StatsService],
  bootstrap: [AppComponent]
})
export class AppModule { }

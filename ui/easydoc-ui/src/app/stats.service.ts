import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ExpenseByTime } from './models';
import { API_HOST } from './constants';
import { MessageService } from './message.service';

@Injectable()
export class StatsService {

  dailyExpense: ExpenseByTime[] = [];

  constructor(
    private http: HttpClient,
    public messageService: MessageService
  ) { }

  updateDailyExpense() {
    this.http.get<ExpenseByTime[]>(`${API_HOST}/stats/daily_expense?start_time=2000-01-01&end_time=2022-01-01`, {
      observe: 'response'
    }).subscribe(
      (res) => {
        this.dailyExpense = res.body;
      },
      (error) => {
        this.messageService.show(`Failed to load daily expense from API`);
      }
    );
  }

}

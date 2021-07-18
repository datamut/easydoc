import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ExpenseByTime } from './models';

@Injectable()
export class StatsService {

  dailyExpense: ExpenseByTime[] = [];

  constructor(private http: HttpClient) { }

  updateDailyExpense() {
    this.http.get<ExpenseByTime[]>('http://localhost:8000/stats/daily_expense?start_time=2000-01-01&end_time=2022-01-01')
      .subscribe(res => {
        this.dailyExpense = res;
      });
  }

}

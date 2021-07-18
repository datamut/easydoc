import { Component, OnInit } from '@angular/core';

import { StatsService } from '../stats.service';

@Component({
  selector: 'app-charts',
  templateUrl: './charts.component.html',
  styleUrls: ['./charts.component.css']
})
export class ChartsComponent implements OnInit {

  constructor(public statsService: StatsService) {
  }

  ngOnInit() {
    this.statsService.updateDailyExpense();
  }

}

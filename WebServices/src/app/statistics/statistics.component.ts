import { Component, OnInit } from '@angular/core';
import { WebApisService } from '../web-apis.service';
import { Metric } from '../metric';

@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.scss']
})
export class StatisticsComponent implements OnInit {

  metrics: any;
  dataTable: any;
  displayedColumns: string[] = ['Service', 'Passedrequests', 'Failedrequests', 'Averagelatency', 'Maxlatency', 'Minlatency'];

  constructor(private webApis: WebApisService) { }

  ngOnInit() {
    this.getMetrics();
  }

  async getMetrics() {
    const metrics = await this.webApis.getMetrics();
    // tslint:disable-next-line:max-line-length
    this.dataTable = [new Metric('convert', metrics.convert.passed, metrics.convert.failed, metrics.convert.avgLatency, metrics.convert.minLatency, metrics.convert.maxLatency),
    // tslint:disable-next-line:max-line-length
    new Metric('rocket', metrics.rocket.passed, metrics.rocket.failed, metrics.rocket.avgLatency, metrics.rocket.minLatency, metrics.rocket.maxLatency),
    new Metric('qr', metrics.qr.passed, metrics.qr.failed, metrics.qr.avgLatency, metrics.qr.minLatency, metrics.qr.maxLatency)];
  }

}

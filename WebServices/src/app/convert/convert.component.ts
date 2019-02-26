import { Component, OnInit } from '@angular/core';
import { WebApisService } from '../web-apis.service';

@Component({
  selector: 'app-convert',
  templateUrl: './convert.component.html',
  styleUrls: ['./convert.component.scss']
})
export class ConvertComponent implements OnInit {

  result: number;
  time: Date;
  rate: number;
  amount = 1;

  constructor(private webApis: WebApisService) { }

  async ngOnInit() {
  }

  async onConvert() {
    const response = await this.webApis.getEurToRon(this.amount);
    console.log(response);
    this.rate = response.rate;
    this.time = response.time;
    this.result = response.converted;
  }

}

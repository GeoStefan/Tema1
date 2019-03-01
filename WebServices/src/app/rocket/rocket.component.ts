import { Component, OnInit } from '@angular/core';
import { Rocket } from '../rocket';
import { WebApisService } from '../web-apis.service';

@Component({
  selector: 'app-rocket',
  templateUrl: './rocket.component.html',
  styleUrls: ['./rocket.component.scss']
})
export class RocketComponent implements OnInit {

  rocketId: string;
  rocket: Rocket;
  pageError: string;

  constructor(private webApis: WebApisService) { }

  ngOnInit() {
    this.rocket = new Rocket();
  }

  async onGetRocket() {
    this.rocket = await this.webApis.getRocket(this.rocketId)
      .catch(error => this.pageError = error);
    if (this.pageError !== undefined) {
      this.pageError = 'Eroare la request';
    }
  }

}

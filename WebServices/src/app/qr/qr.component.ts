import { Component, OnInit } from '@angular/core';
import { WebApisService } from '../web-apis.service';

@Component({
  selector: 'app-qr',
  templateUrl: './qr.component.html',
  styleUrls: ['./qr.component.scss']
})
export class QrComponent implements OnInit {

  qrImage: any;
  image: string;
  size: number;
  rocketName = '';
  loading = false;

  constructor(private webApis: WebApisService) { }

  ngOnInit() {
  }

  async getQr() {
    this.loading = true;
    const rocket = await this.webApis.getRocket(this.rocketName);
    const price = await this.webApis.getEurToRon(rocket.costPerLaunch);
    const data = 'name: ' + rocket.rocketName + ', price: ' + (<string>price.converted) + 'RON';
    this.qrImage = await this.webApis.generateQr(data, this.size);
    this.image = 'data:image/png;base64,' + (<string>this.qrImage.qr).substring(2, (<string>this.qrImage.qr).length - 1);
    this.loading = false;
  }

}

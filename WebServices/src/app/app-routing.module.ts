import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RocketComponent } from './rocket/rocket.component';
import { ConvertComponent } from './convert/convert.component';
import { QrComponent } from './qr/qr.component';
import { StatisticsComponent } from './statistics/statistics.component';

const routes: Routes = [
  { path: 'rocket', component: RocketComponent },
  { path: 'convert', component: ConvertComponent },
  { path: 'qr', component: QrComponent },
  { path: 'statistics', component: StatisticsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

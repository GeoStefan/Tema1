export class Metric {
    constructor(public service: string,
                public passed: number,
                public failed: number,
                public avgLatency: number,
                public minLatency: number,
                public maxLatency: number) { }
}

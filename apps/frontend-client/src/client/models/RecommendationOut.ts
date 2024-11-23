/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ExplainationOut } from './ExplainationOut'

export type RecommendationOut = {
  rec_item_id: number
  rec_item_name: string
  //   rec_item_price: number
  rec_item_imageURL: string
  explanations: Array<ExplainationOut>
}

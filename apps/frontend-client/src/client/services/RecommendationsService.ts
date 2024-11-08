/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RecommendationsOut } from '../models/RecommendationsOut';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class RecommendationsService {

    /**
     * Read Recommendations
     * Retrieve recommended items and explains about recommendation.
     * @returns RecommendationsOut Successful Response
     * @throws ApiError
     */
    public static readRecommendations(): CancelablePromise<RecommendationsOut> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/recommendations/',
        });
    }

}

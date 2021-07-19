export interface ApiResponse {
  status: string;
  message?: string;
}

export interface ExpenseByTime {
  by_time: string,
  total: number
}

export interface ApiError {
  error: string
}

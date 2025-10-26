import { format, formatDistanceToNow, parseISO, isToday, isPast } from 'date-fns';
import { zhCN } from 'date-fns/locale';

export const formatDate = (date: string | Date): string => {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return format(d, 'yyyy-MM-dd', { locale: zhCN });
};

export const formatDateTime = (date: string | Date): string => {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return format(d, 'yyyy-MM-dd HH:mm', { locale: zhCN });
};

export const formatRelativeTime = (date: string | Date): string => {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return formatDistanceToNow(d, { addSuffix: true, locale: zhCN });
};

export const isDateToday = (date: string | Date): boolean => {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return isToday(d);
};

export const isDatePast = (date: string | Date): boolean => {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return isPast(d);
};

